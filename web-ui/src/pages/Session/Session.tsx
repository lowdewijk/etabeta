import {useState} from 'react';
import {useMutation} from 'react-query';
import {useParams} from 'react-router-dom';
import {Box, Button, CircularProgress, TextField} from '@mui/material';
import axios from 'axios';

const asideMainCommonStyles = {
  minHeight: '300px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  padding: '1rem',
  fontWeight: 'bold',
};

interface Message {
  message: string;
  username: string;
}

const sendMessage = async (message: Message) => {
  return axios.post(
    `http://localhost:8000/session/{sessionID}/message`,
    message,
  );
};

export const Session = () => {
  const params = useParams();
  const sessionID = params['id'];

  const [message, setMessage] = useState('');

  const {mutate, isLoading} = useMutation(sendMessage, {
    onSuccess: data => {
      console.log(data);
      alert('message sent');
    },
    onError: () => {
      alert('there was an error');
    },
  });

  function onSend(): void {
    mutate({message, username: 'test'});
  }

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'grid',
        gridTemplateAreas: `"header header"
    "main sidebar"
    "footer footer"`,
        gridTemplateColumns: '1fr minmax(200px, 20%)',
        gridTemplateRows: '3rem 1fr 3rem',
        gap: '1rem',

        '&> *': {
          backgroundColor: '#eee',
        },
      }}
    >
      <Box
        component="header"
        sx={{
          gridArea: 'header',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '0 16px',
        }}
      >
        Welcome to session {sessionID}
      </Box>
      <Box
        component="main"
        sx={{
          gridColumn: 'main',
          ...asideMainCommonStyles,
        }}
      >
        <Box display="flex" flexWrap="wrap" gap={2}>
          chat area
        </Box>
      </Box>
      <Box
        component="aside"
        sx={{
          gridArea: 'sidebar',
          ...asideMainCommonStyles,
        }}
      >
        Sidebar
      </Box>
      <Box
        component="footer"
        sx={{
          gridArea: 'footer',
          fontWeight: 'bold',
          display: 'flex',
          alignItems: 'center',
          padding: '0 16px',
        }}
      >
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
      </Box>
    </Box>
  );
};
