import {FC, useState} from 'react';
import {Button, CircularProgress, TextField} from '@mui/material';

import {useSendMessage} from 'src/api_client/session_queries';

export type ChatInputProps = {
  sessionID: string;
};

export const ChatInput: FC<ChatInputProps> = ({sessionID}) => {
  const [username, setUsername] = useState('');
  const [message, setMessage] = useState('');

  const {mutate: sendMessage, isLoading} = useSendMessage(sessionID);

  function onSend(): void {
    sendMessage({
      message,
      username,
    });
    setMessage('');
  }

  return (
    <>
      <TextField
        variant="standard"
        placeholder="username"
        value={username}
        onChange={event => {
          setUsername(event.target.value);
        }}
      />
      &nbsp;
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
        {isLoading ? <CircularProgress /> : 'Send'}
      </Button>
    </>
  );
};
