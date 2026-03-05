export interface AITool {
  name: string
  category: 'video' | 'image' | 'audio' | 'assistant'
  description: string
  color: string
}

export const aiTools: AITool[] = [
  // Video Generation
  { name: 'Sora', category: 'video', description: 'OpenAI video generation model', color: '#FF3B30' },
  { name: 'Runway', category: 'video', description: 'Gen-3 Alpha video generation', color: '#5E5CE6' },
  { name: 'Kling', category: 'video', description: 'Kuaishou AI video model', color: '#FF9500' },
  { name: 'Seedance', category: 'video', description: 'ByteDance dans ve hareket modeli', color: '#34C759' },
  { name: 'Minimax', category: 'video', description: 'Hailuo AI video generation', color: '#007AFF' },
  { name: 'Pika', category: 'video', description: 'AI video creation platform', color: '#AF52DE' },
  { name: 'Luma', category: 'video', description: 'Dream Machine video AI', color: '#FF2D55' },
  { name: 'Veo', category: 'video', description: 'Google DeepMind video model', color: '#30B0C7' },
  { name: 'Haiper', category: 'video', description: 'Perceptual foundation model', color: '#5856D6' },
  { name: 'Wan', category: 'video', description: 'Alibaba video generation', color: '#FF6B35' },
  { name: 'PixVerse', category: 'video', description: 'AI video creation tool', color: '#00C7BE' },
  // Image Generation
  { name: 'Midjourney', category: 'image', description: 'AI gorsel uretim platformu', color: '#1D1D1F' },
  { name: 'DALL-E', category: 'image', description: 'OpenAI gorsel modeli', color: '#10A37F' },
  { name: 'Stable Diffusion', category: 'image', description: 'Acik kaynakli gorsel AI', color: '#A855F7' },
  { name: 'Flux', category: 'image', description: 'Black Forest Labs modeli', color: '#EC4899' },
  { name: 'Ideogram', category: 'image', description: 'AI gorsel + tipografi', color: '#F59E0B' },
  { name: 'Imagen', category: 'image', description: 'Google gorsel modeli', color: '#4285F4' },
  // Audio
  { name: 'Suno', category: 'audio', description: 'AI muzik uretimi', color: '#1DB954' },
  { name: 'Udio', category: 'audio', description: 'AI muzik platformu', color: '#8B5CF6' },
  { name: 'ElevenLabs', category: 'audio', description: 'AI ses sentezi', color: '#1D1D1F' },
  // Assistants
  { name: 'ChatGPT', category: 'assistant', description: 'OpenAI asistan', color: '#10A37F' },
  { name: 'Claude', category: 'assistant', description: 'Anthropic asistani', color: '#D97706' },
  { name: 'Gemini', category: 'assistant', description: 'Google AI asistani', color: '#4285F4' },
  { name: 'Topaz', category: 'assistant', description: 'AI video/gorsel iyilestirme', color: '#F97316' },
  { name: 'CapCut AI', category: 'assistant', description: 'AI video duzenleme', color: '#000000' },
]

export const toolCategories = [
  { id: 'video', label: 'Video Uretim', color: '#FF3B30', count: 11 },
  { id: 'image', label: 'Gorsel Uretim', color: '#5E5CE6', count: 6 },
  { id: 'audio', label: 'Ses/Muzik', color: '#34C759', count: 3 },
  { id: 'assistant', label: 'Yardimci AI', color: '#FF9500', count: 5 },
]
