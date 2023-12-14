import {FC} from 'react';
import {useQuery} from 'react-query';
import {CircularProgress} from '@mui/material';

import {getMessages} from 'src/api_client/session';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type ChatDisplayProps = {
  sessionID: string;
};

export const ChatDisplay: FC<ChatDisplayProps> = ({sessionID}) => {
  const {
    data: messages,
    isError,
    isLoading,
  } = useQuery(['messages', sessionID], () => getMessages(sessionID), {});

  return (
    <div>
      {isLoading ? (
        <div>
          Loading messages: <CircularProgress />
        </div>
      ) : isError ? (
        <ErrorContainer>Error loading messages.</ErrorContainer>
      ) : (
        messages?.map((message, idx) => (
          <div key={idx}>
            <div>{message.username}</div>
            <div>{message.message}</div>
          </div>
        ))
      )}
    </div>
  );
};
