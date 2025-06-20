import { marked } from 'marked';

class AIService {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:1234';
  }

//   `You are a helpful assistant that helps users with their notes. 
          
// Please format your responses using markdown formatting:
// - Use **bold** for emphasis
// - Use *italics* for subtle emphasis  
// - Use \`code\` for technical terms
// - Use # ## ### for headings when appropriate
// - Use - or * for bullet points
// - Separate different topics with blank lines

// Keep responses clear, well-structured, and properly formatted.`


  async generateFormattedText(prompt, context = '', model = 'llama-3.2-3b-instruct') {
    try {
      const markdownText = await this.generateText(prompt, context, model);
      
      // Convert markdown to HTML
      const htmlContent = marked(markdownText);
      
      return {
        markdown: markdownText,
        html: htmlContent
      };
    } catch (error) {
      console.error('AI Service Error:', error);
      throw error;
    }
  }

  async generateText(prompt, context = '', model = 'llama-3.2-3b-instruct') {
    try {
      const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: model, // LM Studio usually uses this
          messages: [
            {
              role: 'system',
              content: `You are a tool to complete the required prompt. Do not be conversational and only respond with the CONCISE requested text, make responses minimal length unless asked otherwise. 
          
Please format your responses using markdown formatting:
- Use **bold** for emphasis
- Use *italics* for subtle emphasis  
- Use \`code\` for technical terms
- Use # ## ### for headings when appropriate
- Use - for bullet points
- Use 1. 2. 3. etc for numbered lists
- Separate different topics with blank lines
- use > for quotes
- use --- for horizontal lines
- FOR ANY MATHEMTICAL TERMS USE KATEX FORMATTING and wrap with "$"before and "$" after the term, e.g. "$E=mc^2$", NEVER USE "$$"
- FOR ANY Chemical TERMS USE  mhchem for KaTeX FORMATTING and wrap with $\\ce{ before and }$ after the term, e.g. "$\\ce{CH_3CHO + H_2O -> CH_3C(O)H}$"
Keep responses clear, well-structured, and properly formatted.`
            },
            ...(context ? [{
              role: 'user',
              content: `Context from my notes: ${context}`
            }] : []),
            {
              role: 'user',
              content: prompt
            }
          ],
          temperature: 0.7,
          max_tokens: 1000,
          stream: false
        })
      });

      console.error('Response Status:', response);

      if (!response.ok) {
        throw new Error(`AI service error: ${response.status}`);
      }

      const data = await response.json();
      return data.choices[0]?.message?.content || 'No response generated';
    } catch (error) {
      console.error('AI Service Error:', error);
      throw new Error('Failed to connect to local AI model. Make sure LM Studio is running on port 1234.');
    }
  }

  async isAvailable() {
    try {
      const response = await fetch(`${this.baseUrl}/v1/models`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      return response.ok;
    } catch (error) {
      return false;
    }
  }

  async getModels() {
    try {
      const response = await fetch(`${this.baseUrl}/v1/models`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        }
      });

      if (!response.ok) {
        throw new Error(`Failed to fetch models: ${response.status}`);
      }

      const data = await response.json();
      const modelIds = data.data.map(model => model.id);
      return modelIds || [];
    } catch (error) {
      console.error('Error fetching models:', error);
      throw new Error('Failed to fetch models from AI service.');
    }
  }
}

export const aiService = new AIService();