// mock_env.js
// RPG Maker MZ Mock Environment for Node.js Testing

global.window = global;
global.console = console;

// Math / Utils
global.Utils = {
  encodeURI: (s) => s
};

// Managers & Core
global.Input = { keyMapper: {}, gamepadMapper: {}, isTriggered: () => false };
global.TouchInput = { isTriggered: () => false, isPressed: () => false, x: 0, y: 0 };
global.AudioManager = {
  playSe: () => {},
  createBuffer: () => {},
  stopSe: () => {}
};
global.ImageManager = {
  loadPicture: () => ({ addLoadListener: () => {} }),
  loadSystem: () => ({ addLoadListener: () => {} })
};
global.SceneManager = {
  _scene: {},
  goto: () => {}
};
global.Graphics = { width: 816, height: 624 };

// Sprite
global.Sprite = class {
  constructor() {
    this.bitmap = null;
    this.anchor = { x: 0, y: 0 };
    this.scale = { x: 1, y: 1 };
  }
};
global.Bitmap = class {
  constructor() {
    this.fontFace = '';
    this.fontSize = 28;
    this.textColor = '#ffffff';
  }
  measureTextWidth() { return 100; }
  drawText() {}
};

// Game Objects
global.$gameMap = {
  events: () => [],
  isEventRunning: () => false
};

global.$gamePlayer = {
  _x: 5, _y: 5,
  isMoving: () => false,
  _direction: 2,
  requestAnimation: () => {}
};

global.$gameMessage = {
  isBusy: () => false
};

global.$gameVariables = {
  _data: [],
  value: function(id) { return this._data[id] || 0; },
  setValue: function(id, val) { this._data[id] = val; }
};

global.$gameTemp = {
  requestAnimation: () => {}
};

global.$gameScreen = {
  startShake: () => {},
  startFlash: () => {}
};

global.$gameParty = {
  leader: () => ({
    gainHp: () => {},
    isDead: () => false
  })
};

global.$gameSystem = {
  isJapanese: () => true
};

global.$gameSelfSwitches = {
  setValue: () => {}
};

// Shorthand function used by ABS_Ultimate.js
global._ = (o) => o;
global.R = (v, def = 0) => (v !== undefined && v !== null && !isNaN(v) ? v : def);
