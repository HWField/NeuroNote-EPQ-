import { Node } from '@tiptap/core'
import { VueNodeViewRenderer } from '@tiptap/vue-3'
import WhiteboardNodeView from './WhiteboardPreview.vue'

export const WhiteboardExtension = Node.create({
  name: 'whiteboard',
  
  group: 'block',
  atom: true,
  selectable: true,
  draggable: true,
  
  parseHTML() {
    return [
      { 
        tag: 'div[data-type="whiteboard"]',
        getAttrs: element => {
          // Parse viewport if it exists
          let viewport = null;
          const viewportAttr = element.getAttribute('data-viewport');
          if (viewportAttr) {
            try {
              viewport = JSON.parse(viewportAttr);
            } catch (e) {
              viewport = null;
            }
          }
          
          return {
            id: element.getAttribute('data-id'),
            name: element.getAttribute('data-name'),
            background: element.getAttribute('data-background'),
            parentTab: element.getAttribute('data-parent-tab'),
            viewport: viewport
          };
        },
      },
    ]
  },
  
  renderHTML({ HTMLAttributes }) {
    const attrs = { 
      'data-type': 'whiteboard',
      'data-id': HTMLAttributes.id,
      'data-name': HTMLAttributes.name,
      'data-background': HTMLAttributes.background,
      class: 'whiteboard-node'
    };
    
    if (HTMLAttributes.parentTab) {
      attrs['data-parent-tab'] = HTMLAttributes.parentTab;
    }
    
    if (HTMLAttributes.viewport) {
      attrs['data-viewport'] = JSON.stringify(HTMLAttributes.viewport);
    }
    
    return [
      'div', 
      attrs,
      ['div', { class: 'whiteboard-container' }]
    ];
  },
  
  addAttributes() {
    return {
      id: {
        default: null,
      },
      name: {
        default: 'Untitled Whiteboard',
      },
      background: {
        default: 'sGrid',
      },
      parentTab: {
        default: null,
      },
      viewport: {
        default: null,
      }
    }
  },
  
  addNodeView() {
    return VueNodeViewRenderer(WhiteboardNodeView)
  },
})