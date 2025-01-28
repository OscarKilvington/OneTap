import React from 'react';
import { Box, Paper, Typography, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

interface FilePreviewProps {
  file: File;
  onRemove: () => void;
}

const FilePreview: React.FC<FilePreviewProps> = ({ file, onRemove }) => {
  const isImage = file.type.startsWith('image/');

  return (
    <Paper
      sx={{
        p: 1,
        mb: 2,
        display: 'flex',
        alignItems: 'center',
        gap: 1,
        backgroundColor: 'grey.100',
      }}
    >
      {isImage && (
        <Box
          component="img"
          src={URL.createObjectURL(file)}
          alt={file.name}
          sx={{
            width: 50,
            height: 50,
            objectFit: 'cover',
            borderRadius: 1,
          }}
        />
      )}
      <Box sx={{ flexGrow: 1 }}>
        <Typography variant="body2" noWrap>
          {file.name}
        </Typography>
        <Typography variant="caption" color="textSecondary">
          {(file.size / 1024).toFixed(1)} KB
        </Typography>
      </Box>
      <IconButton size="small" onClick={onRemove}>
        <CloseIcon fontSize="small" />
      </IconButton>
    </Paper>
  );
};

export default FilePreview;