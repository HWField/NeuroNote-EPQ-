import { Extension } from '@tiptap/core'
import Suggestion from '@tiptap/suggestion'
import { PluginKey } from 'prosemirror-state'

export const tagSuggestionKey = new PluginKey('tagSuggestion')

export const Tags = Extension.create({
  name: 'tags',

  addOptions() {
    return {
      suggestion: {
        char: '@',
        command: ({ editor, range, props }) => {
          console.error("Tag props received:", props);
          
          // We need to first delete the @ trigger character
          editor
            .chain()
            .focus()
            .deleteRange({ from: range.from - 1, to: range.to })
            .insertContent([{
                type: 'text',
                text: ' ' // Insert space as separate text node
              },{
              type: 'mention',
              attrs: {
                id: props.id,
                label: props.title
              }
            },
            {
                type: 'text',
                text: ' ' // Insert space as separate text node
              }])
            .run();
        },
      },
    }
  },

  addProseMirrorPlugins() {
    return [
      Suggestion({
        editor: this.editor,
        ...this.options.suggestion,
        pluginKey: tagSuggestionKey,
      }),
    ]
  },
})