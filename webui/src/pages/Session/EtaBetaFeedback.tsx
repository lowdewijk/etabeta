import {FC} from 'react';
import {Box, CircularProgress} from '@mui/material';

import {useGetEtaBetaState} from 'src/api_client/session_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';
import {EtaBetaStateDisplay} from './EtaBetaStateDisplay';

export type EtaBetaFeedbackProps = {
  sessionID: string;
};

export const EtaBetaFeedback: FC<EtaBetaFeedbackProps> = ({sessionID}) => {
  const {
    data: etabetaState,
    isLoading,
    isError,
  } = useGetEtaBetaState(sessionID);

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        fontSize: '0.8rem',
        overflow: 'auto',
        maxHeight: '100%',
      }}
    >
      <Box>
        <h1>Eta Beta</h1>
      </Box>
      <Box
        sx={{
          paddingTop: '10px',
          fontWeight: 'normal',
        }}
      >
        <div>
          {isLoading || !etabetaState ? (
            <div>
              Loading messages: <CircularProgress />
            </div>
          ) : isError ? (
            <ErrorContainer>Error loading messages.</ErrorContainer>
          ) : (
            <EtaBetaStateDisplay state={etabetaState} />
          )}
        </div>
      </Box>
    </Box>
  );
};
