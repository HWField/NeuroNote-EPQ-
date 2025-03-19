import { ref } from 'vue';

// Simple event bus for cross-component communication
export const eventBus = {
  // Store for handlers
  _events: {},
  
  // Register an event handler
  on(event, handler) {
    if (!this._events[event]) {
      this._events[event] = [];
    }
    this._events[event].push(handler);
  },
  
  // Remove an event handler
  off(event, handler) {
    if (!this._events[event]) return;
    if (!handler) {
      delete this._events[event];
    } else {
      this._events[event] = this._events[event].filter(h => h !== handler);
    }
  },
  
  // Emit an event
  emit(event, ...args) {
    if (!this._events[event]) return;
    this._events[event].forEach(handler => handler(...args));
  }
};