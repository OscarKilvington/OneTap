import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, SelectChangeEvent } from '@mui/material';

interface Model {
  id: string;
  name: string;
  category: string;
  priority: number;
}

interface ModelSelectorProps {
  currentModel: string;
  onModelChange: (modelId: string) => void;
}

const SAMPLE_MODELS: Model[] = [
  { id: 'gpt4', name: 'GPT-4 Turbo', category: 'OpenAI', priority: 5 },
  { id: 'gpt35', name: 'GPT-3.5 Turbo', category: 'OpenAI', priority: 4 },
  { id: 'claude3', name: 'Claude 3 Opus', category: 'Anthropic', priority: 5 },
  { id: 'claude2', name: 'Claude 2.1', category: 'Anthropic', priority: 4 },
];

const ModelSelector: React.FC<ModelSelectorProps> = ({ currentModel, onModelChange }) => {
  const handleChange = (event: SelectChangeEvent) => {
    onModelChange(event.target.value);
  };

  return (
    <FormControl fullWidth variant="outlined" size="small">
      <InputLabel>AI Model</InputLabel>
      <Select
        value={currentModel}
        onChange={handleChange}
        label="AI Model"
      >
        {SAMPLE_MODELS.map((model) => (
          <MenuItem key={model.id} value={model.id}>
            {model.name}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default ModelSelector;