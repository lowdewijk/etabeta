import {FC, useState} from 'react';
import {useMutation} from 'react-query';
import {toast} from 'react-toastify';
import {Button, CircularProgress, TextField} from '@mui/material';

import {Message, sendMessage} from 'src/api_client/session';

export type ChatInputProps = {
  sessionID: string;
};

export const ChatInput: FC<ChatInputProps> = ({sessionID}) => {
  const [message, setMessage] = useState('');

  const {mutate, isLoading} = useMutation(
    (msg: Message) => sendMessage(sessionID, msg),
    {
      onError: (error: Error) => {
        toast.error('Error sending message: ' + error.message);
      },
    },
  );

  function onSend(): void {
    mutate({
      message,
      username: 'test',
    });
  }

  return (
    <>
      <TextField
        variant="standard"
        fullWidth
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
