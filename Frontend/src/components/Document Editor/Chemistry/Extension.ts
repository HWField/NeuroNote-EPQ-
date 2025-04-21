import { mergeAttributes, Node } from '@tiptap/core'
import { VueNodeViewRenderer } from '@tiptap/vue-3'

import Component from './Component.vue'

export default Node.create({
  name: 'chemistry',

  group: 'block',

  atom: true,

  addAttributes() {
    return {
      moleculeData: {
        default: null,
      },
      format: {
        default: 'mol',
      },
      is3D: {
        default: true
      },
      height: {
        default: 250
      }
    }
  },

  parseHTML() {
    return [
      {
        tag: 'div[data-type="chemistry-component"]',
      },
    ]
  },

  renderHTML({ HTMLAttributes }) {
    return ['div', mergeAttributes({
      'data-type': 'chemistry-component'
    }, HTMLAttributes)]
  },

  addNodeView() {
    return VueNodeViewRenderer(Component)
  },
})