import {FC} from 'react';
import {Box, CircularProgress} from '@mui/material';

import {useGetEtaBetaMessages} from 'src/api_client/session_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type EtaBetaFeedbackProps = {
  sessionID: string;
};

export const EtaBetaFeedback: FC<EtaBetaFeedbackProps> = ({sessionID}) => {
  const {data: messages, isLoading, isError} = useGetEtaBetaMessages(sessionID);

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
      <Box sx={{'padding-top': '10px'}}>
        <div>
          {isLoading || !messages ? (
            <div>
              Loading messages: <CircularProgress />
            </div>
          ) : isError ? (
            <ErrorContainer>Error loading messages.</ErrorContainer>
          ) : (
            messages
              .sort((a, b) => b.timestamp - a.timestamp)
              .map((message, idx) => (
                <Box
                  key={idx}
                  sx={{
                    p: 1,
                    m: 1,
                    bgcolor: 'background.paper',
                    borderRadius: 1,
                  }}
                >
                  {message.message}
                </Box>
              ))
          )}
        </div>
      </Box>
    </Box>
  );
};
