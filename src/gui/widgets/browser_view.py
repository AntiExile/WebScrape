from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import pyqtSignal, QObject, Qt
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtGui import QPalette, QColor

class InteractionRecorder(QObject):
    interaction_recorded = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.recording = False
        self.interactions = []

class BrowserView(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.recorder = InteractionRecorder()
        self.channel = QWebChannel()
        self.page().setWebChannel(self.channel)
        self.channel.registerObject("recorder", self.recorder)
        self.page().loadFinished.connect(self.inject_tracking_code)
        
        # Set transparent background until page loads
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(40, 30, 60))  # Dark theme base color
        self.setPalette(palette)
        
        # Add custom CSS for web content background
        self.page().setBackgroundColor(QColor(40, 30, 60))
        
        # Enable settings with correct WebAttribute enum
        settings = self.page().settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = self.page().createStandardContextMenu()
        menu.addSeparator()
        inspect_action = menu.addAction("Inspect Element")
        inspect_action.triggered.connect(
            lambda: self.page().triggerAction(
                self.page().WebAction.InspectElement
            )
        )
        menu.exec(self.mapToGlobal(position))

    def inject_tracking_code(self):
        js_code = """
        new QWebChannel(qt.webChannelTransport, function(channel) {
            window.recorder = channel.objects.recorder;
            
            document.addEventListener('click', function(e) {
                if (!window.recorder.recording) return;
                let xpath = getXPath(e.target);
                window.recorder.interaction_recorded.emit({
                    'type': 'click',
                    'xpath': xpath,
                    'text': e.target.textContent,
                    'tag': e.target.tagName
                });
            });
            
            document.addEventListener('input', function(e) {
                if (!window.recorder.recording) return;
                let xpath = getXPath(e.target);
                window.recorder.interaction_recorded.emit({
                    'type': 'input',
                    'xpath': xpath,
                    'value': e.target.value
                });
            });
            
            function getXPath(element) {
                if (element.id !== '')
                    return `//*[@id="${element.id}"]`;
                if (element === document.body)
                    return '/html/body';
                
                let ix = 0;
                let siblings = element.parentNode.childNodes;
                
                for (let i = 0; i < siblings.length; i++) {
                    let sibling = siblings[i];
                    if (sibling === element)
                        return getXPath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName)
                        ix++;
                }
            }
        });
        """
        self.page().runJavaScript(js_code)
        self.recorder.recording = True