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
  { id: 'gpt4', name: 'GPT-4', category: 'Programming', priority: 5 },
  { id: 'claude', name: 'Claude', category: 'Creative Writing', priority: 4 },
  { id: 'dalle', name: 'DALL-E', category: 'Image Generation', priority: 5 },
  { id: 'mathpix', name: 'Mathpix', category: 'Math', priority: 4 },
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
            {model.name} - {model.category}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default ModelSelector;