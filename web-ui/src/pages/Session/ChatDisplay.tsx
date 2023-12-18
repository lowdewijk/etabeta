import {FC} from 'react';
import {CircularProgress} from '@mui/material';

import {useGetSessionMessages} from 'src/api_client/session_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';

export type ChatDisplayProps = {
  sessionID: string;
};

export const ChatDisplay: FC<ChatDisplayProps> = ({sessionID}) => {
  const {data: messages, isError, isLoading} = useGetSessionMessages(sessionID);

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
