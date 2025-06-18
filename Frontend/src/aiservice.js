class AIService {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:1234';
  }

  async generateText(prompt, context = '') {
    try {
      const response = await fetch(`${this.baseUrl}/v1/chat/completions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model: 'llama-3.2-3b-instruct', // LM Studio usually uses this
          messages: [
            {
              role: 'system',
              content: `You are a helpful assistant that helps users with their notes. 
          
Please format your responses using markdown formatting:
- Use **bold** for emphasis
- Use *italics* for subtle emphasis  
- Use \`code\` for technical terms
- Use # ## ### for headings when appropriate
- Use - or * for bullet points
- Separate different topics with blank lines

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
}

export const aiService = new AIService();