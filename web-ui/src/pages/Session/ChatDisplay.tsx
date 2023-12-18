import {FC} from 'react';
import {Box, CircularProgress} from '@mui/material';

import {useGetSessionMessages} from 'src/api_client/session_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type ChatDisplayProps = {
  sessionID: string;
};

export const ChatDisplay: FC<ChatDisplayProps> = ({sessionID}) => {
  const {data: messages, isError, isLoading} = useGetSessionMessages(sessionID);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
      }}
    >
      {isLoading ? (
        <div>
          Loading messages: <CircularProgress />
        </div>
      ) : isError ? (
        <ErrorContainer>Error loading messages.</ErrorContainer>
      ) : (
        messages?.map((message, idx) => (
          <Box
            key={idx}
            sx={{p: 1, m: 1, bgcolor: 'background.paper', borderRadius: 1}}
          >
            <div style={{textAlign: 'left'}}>
              {message.username} : {message.message}
            </div>
          </Box>
        ))
      )}
    </div>
  );
};
