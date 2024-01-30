import React, {ReactNode} from 'react';
import {Alert} from '@mui/material';

export const ErrorContainer: React.FC<{children: ReactNode}> = ({children}) => {
  return <Alert severity="error">{children}</Alert>;
};
