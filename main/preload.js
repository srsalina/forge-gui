// main/preload.js

const { contextBridge, ipcRenderer } = require('electron');

// Expose a limited set of APIs to the renderer process
contextBridge.exposeInMainWorld('api', {
  // Example: Send data to the main process
  send: (channel, data) => {
    // Whitelisted channels
    const validChannels = ['toMain'];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },

  // Example: Receive data from the main process
  receive: (channel, func) => {
    const validChannels = ['fromMain'];
    if (validChannels.includes(channel)) {
      // Remove the listener when it's no longer needed to prevent memory leaks
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
  },
});
