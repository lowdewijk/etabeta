import {FC} from 'react';
import {Link} from 'react-router-dom';
import {Box} from '@mui/material';

import {MenuAppBar} from 'src/components/MenuAppBar/MenuAppBar';
import {ROUTE_SESSIONS} from 'src/routes/Routes';
import {ChatDisplay} from './ChatDisplay';
import {ChatInput} from './ChatInput';
import {EtaBetaFeedback} from './EtaBetaFeedback';

const asideMainCommonStyles = {
  minHeight: '300px',
  display: 'flex',
  padding: '1rem',
  fontWeight: 'bold',
};

export type SessionProps = {
  sessionID: string;
};

export const SessionPage: FC<SessionProps> = ({sessionID}) => {
  return (
    <Box
      sx={{
        height: '100vh',
        display: 'grid',
        gridTemplateAreas: `"header header"
                            "main sidebar"
                            "footer footer"`,
        gridTemplateColumns: '1fr minmax(300px, 20%)',
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
          padding: '0 0px',
        }}
      >
        <MenuAppBar
          parentPage={<Link to={ROUTE_SESSIONS}>Sessions</Link>}
          pageName={`Session: ${sessionID}`}
        />
      </Box>
      <Box
        component="main"
        sx={{
          gridColumn: 'main',
          alignItems: 'left',
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
        <EtaBetaFeedback sessionID={sessionID} />
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
