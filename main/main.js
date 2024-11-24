const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

// Determine which URL or file to load
if (process.env.NODE_ENV === 'development') {
  console.log('Loading from Vite server...')
  mainWindow.loadURL('http://localhost:5173');  // Ensure the Vite server is running on this port
} else {
  ('Loading from built files...')
  mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));  // Load from the dist folder
}
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
///////////////////////////////
//////////////////////////////////////////////
//////////////////////////////////
///////////////////////////////
//////////////////////////////
///////////////////