import { VueRenderer } from '@tiptap/vue-3'
import tippy from 'tippy.js'
import TagsList from './TagsList.vue'
import { computed } from "vue";
import { useGraphStore } from '@/stores/useGraphStore'
export default {

  char: '@',
  items: ({ query }) => {
    // Get the graph store
    const graphStore = useGraphStore()
    
    const tagElements = computed(() => 
      graphStore.elements.filter((el) => el.type === "tag")
    );

    // Filter elements to only include tag nodes
    console.log('Graph store:', tagElements.value)
    
    // Return filtered tags based on query
    return tagElements.value
      .filter(tag => tag.name.toLowerCase().includes(query.toLowerCase()))
      .slice(0, 5)
      .map(tag => ({
        id: tag.data.id,        // Store the tag ID
        title: tag.name   // Store the tag title for display
      }))
  },

  render: () => {
    let component
    let popup

    return {
      onStart: props => {
        component = new VueRenderer(TagsList, {
          props,
          editor: props.editor,
        })

        if (!props.clientRect) {
          return
        }

        popup = tippy('body', {
          getReferenceClientRect: props.clientRect,
          appendTo: () => document.body,
          content: component.element,
          showOnCreate: true,
          interactive: true,
          trigger: 'manual',
          placement: 'bottom-start',
        })
      },

      onUpdate(props) {
        component.updateProps(props)

        if (!props.clientRect) {
          return
        }

        popup[0].setProps({
          getReferenceClientRect: props.clientRect,
        })
      },

      onKeyDown(props) {
        if (props.event.key === 'Escape') {
          popup[0].hide()
          return true
        }

        return component.ref?.onKeyDown(props)
      },

      onExit() {
        popup[0].destroy()
        component.destroy()
      },
    }
  },
  
  // This is the command handler that was missing
  command: ({ editor, range, props }) => {
    const nodeAfter = editor.view.state.selection.$to.nodeAfter
    const overrideSpace = nodeAfter?.text?.startsWith(' ')
    
    if (overrideSpace) {
      range.to += 1
    }

    editor
      .chain()
      .focus()
      .deleteRange(range)
      .insertContent([
        {
          type: 'mention',
          attrs: {
            id: props.id,
            label: props.id,
          },
        },
        {
          type: 'text',
          text: ' ',
        },
      ])
      .run()
  },
}