import {FC} from 'react';
import {Box} from '@mui/material';

import {ChatDisplay} from './ChatDisplay';
import {ChatInput} from './ChatInput';

const asideMainCommonStyles = {
  minHeight: '300px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '1rem',
  fontWeight: 'bold',
};

export interface SessionProps {
  sessionID: string;
}

export const Session: FC<SessionProps> = ({sessionID}) => {
  return (
    <Box
      sx={{
        height: '100vh',
        display: 'grid',
        gridTemplateAreas: `"header header"
    "main sidebar"
    "footer footer"`,
        gridTemplateColumns: '1fr minmax(200px, 20%)',
        gridTemplateRows: '3rem 1fr 3rem',
        gap: '1rem',

        '&> *': {
          backgroundColor: '#eee',
        },
      }}
    >
      <Box
        component="header"
        sx={{
          gridArea: 'header',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '0 16px',
        }}
      >
        Welcome to session {sessionID}
      </Box>
      <Box
        component="main"
        sx={{
          gridColumn: 'main',
          ...asideMainCommonStyles,
        }}
      >
        <Box display="flex" flexWrap="wrap" gap={2}>
          <ChatDisplay sessionID={sessionID} />
        </Box>
      </Box>
      <Box
        component="aside"
        sx={{
          gridArea: 'sidebar',
          ...asideMainCommonStyles,
        }}
      >
        Sidebar
      </Box>
      <Box
        component="footer"
        sx={{
          gridArea: 'footer',
          fontWeight: 'bold',
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
        }}
      >
        <ChatInput sessionID={sessionID} />
      </Box>
    </Box>
  );
};
