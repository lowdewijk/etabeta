import {FC, useEffect, useRef} from 'react';
import {Box, CircularProgress} from '@mui/material';

import {
  useGetEtaBetaState,
  useReadMessages,
} from 'src/api_client/session_queries';
import {useLoggedInAuth} from 'src/auth/AuthProvider';
import {DisplayTime} from 'src/components/DisplayTime/DisplayTime';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type ChatDisplayProps = {
  sessionID: string;
};

export const ChatDisplay: FC<ChatDisplayProps> = ({sessionID}) => {
  const {username} = useLoggedInAuth();

  const {
    data: messages,
    isError,
    isLoading,
  } = useReadMessages(sessionID, username);

  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
    }
  }, [messages]);

  const {data: etabetaState} = useGetEtaBetaState(sessionID);

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'flex-start',
        overflow: 'auto',
        maxHeight: '100%',
        width: '100%',
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
            sx={{
              p: 1,
              m: 1,
              bgcolor:
                message.username === 'Eta Beta'
                  ? '#e0e0e0'
                  : 'background.paper',
              borderRadius: 1,
              fontWeight: 'normal',
              width: '90%',
              marginLeft: message.username === username ? undefined : 'auto',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'flex-end',
            }}
          >
            <Box sx={{}}>
              <b>{message.username}</b>: {message.message}
              {(etabetaState?.under_observation ?? []).includes(
                message.timestamp,
              ) ? (
                <span>&nbsp; 👀</span>
              ) : null}
            </Box>
            <Box
              sx={{
                paddingLeft: '1rem',
                whiteSpace: 'nowrap',
                fontSize: '0.8rem',
              }}
            >
              <DisplayTime timestamp={message.timestamp} />
            </Box>
          </Box>
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};
