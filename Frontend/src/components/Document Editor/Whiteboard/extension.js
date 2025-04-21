import { Node } from '@tiptap/core'
import { VueNodeViewRenderer } from '@tiptap/vue-3'
import WhiteboardNodeView from './WhiteboardPreview.vue'

export const WhiteboardExtension = Node.create({
  name: 'whiteboard',
  
  // Group it with other block elements like paragraphs, headings, etc.
  group: 'block',
  
  // Make it a self-contained element
  atom: true,
  
  // It should be selectable as one unit
  selectable: true,
  
  // Prevent dragging content into or out of this node
  draggable: true,
  
  // Define HTML parsing rules
  parseHTML() {
    return [
      { 
        tag: 'div[data-type="whiteboard"]',
        getAttrs: element => ({
          id: element.getAttribute('data-id'),
          name: element.getAttribute('data-name'),
          background: element.getAttribute('data-background')
        }),
      },
    ]
  },
  
  // Define how to render the node to HTML
  renderHTML({ HTMLAttributes }) {
    return [
      'div', 
      { 
        'data-type': 'whiteboard',
        'data-id': HTMLAttributes.id,
        'data-name': HTMLAttributes.name,
        'data-background': HTMLAttributes.background,
        class: 'whiteboard-node'
      },
      ['div', { class: 'whiteboard-container' }]
    ]
  },
  
  // Define attributes that can be stored with the node
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
      }
    }
  },
  
  // Define how to render this node in the editor using the Vue component
  addNodeView() {
    return VueNodeViewRenderer(WhiteboardNodeView)
  },
})