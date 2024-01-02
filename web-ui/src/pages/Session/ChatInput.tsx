import {FC, useState} from 'react';
import {Navigate} from 'react-router-dom';
import {Button, TextField} from '@mui/material';

import {useSendMessage} from 'src/api_client/session_queries';
import {useAuth} from 'src/auth/AuthProvider';
import {ROUTE_LOGIN} from 'src/routes/Routes';

export type ChatInputProps = {
  sessionID: string;
};

export const ChatInput: FC<ChatInputProps> = ({sessionID}) => {
  const {username} = useAuth();
  const [message, setMessage] = useState('');

  const {mutate: sendMessage, isLoading} = useSendMessage(sessionID);

  // this code is really only for the type checker
  if (username === undefined) {
    return <Navigate to={ROUTE_LOGIN} />;
  }
  const usernameDefined = username;

  function onSend(): void {
    sendMessage({
      message,
      username: usernameDefined,
    });
    setMessage('');
  }

  return (
    <>
      <TextField
        variant="standard"
        fullWidth
        value={message}
        onChange={event => {
          setMessage(event.target.value);
        }}
        onKeyDown={event => {
          const modifierKeyWasPressed = event.metaKey || event.ctrlKey;
          const enterWasPressed = event.key === 'Enter';
          if (modifierKeyWasPressed && enterWasPressed) {
            event.preventDefault();
            onSend();
          }
        }}
      />
      <Button variant="contained" onClick={onSend}>
        {isLoading ? 'Sending..' : 'Send'}
      </Button>
    </>
  );
};
