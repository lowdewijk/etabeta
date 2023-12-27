import {FC, useEffect, useRef} from 'react';
import {Box, CircularProgress} from '@mui/material';

import {useGetMessages} from 'src/api_client/session_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type ChatDisplayProps = {
  sessionID: string;
};

export const ChatDisplay: FC<ChatDisplayProps> = ({sessionID}) => {
  const {data: messages, isError, isLoading} = useGetMessages(sessionID);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
    }
  }, [messages]);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        overflow: 'auto',
        maxHeight: '100%',
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
            {message.username} : {message.message}
          </Box>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};
