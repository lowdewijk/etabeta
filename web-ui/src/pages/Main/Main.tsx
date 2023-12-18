import {useState} from 'react';
import {Box, Button, CircularProgress, TextField} from '@mui/material';

import {
  useCreateSession,
  useDeleteSession,
  useListSessions,
} from 'src/api_client/session_queries';

export const Main = () => {
  const {data: sessions, isError, isLoading} = useListSessions();
  const {mutate: createSession, isLoading: isCreateSessionLoading} =
    useCreateSession();
  const {mutate: deleteSession, isLoading: isDeletingSession} =
    useDeleteSession();
  const [newSessionId, setNewSessionId] = useState('');

  const onSessionDelete = (id: string) => deleteSession(id);

  const onCreateSession = () => {
    createSession(newSessionId);
    setNewSessionId('');
  };

  return (
    <Box>
      Choose a debate session:
      <ul>
        {isLoading || isCreateSessionLoading || isDeletingSession ? (
          <div>
            <CircularProgress />
          </div>
        ) : isError ? (
          <div>Error loading sessions.</div>
        ) : (
          sessions?.map((session, idx) => (
            <li key={idx}>
              <span>
                <a href={`session/${session.id}`}>{session.id}</a>
              </span>
              <span>
                <Button onClick={() => onSessionDelete(session.id)}>
                  DELETE
                </Button>
              </span>
            </li>
          ))
        )}
      </ul>
      <div>
        <TextField
          variant="standard"
          value={newSessionId}
          onChange={event => {
            setNewSessionId(event.target.value);
          }}
        />
        <Button variant="contained" onClick={onCreateSession}>
          CREATE
        </Button>
      </div>
    </Box>
  );
};
