import {useState} from 'react';
import {Link} from 'react-router-dom';
import DeleteIcon from '@mui/icons-material/Delete';
import {Button, CircularProgress, TextField} from '@mui/material';

import {
  useCreateSession,
  useDeleteSession,
  useListSessions,
} from 'src/api_client/sessions_queries';
import {ErrorContainer} from 'src/components/Error/ErrorContainer';
import {MenuPage} from 'src/components/MenuPage/MenuPage';

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
    <MenuPage pageName="Session overview">
      <div
        style={{
          paddingLeft: '1rem',
        }}
      >
        <p
          style={{
            paddingTop: '1rem',
            paddingBottom: '1rem',
          }}
        >
          Choose a session to join or create a new one by entering a session.
        </p>
        <ul
          style={{
            marginLeft: '1rem',
          }}
        >
          {isLoading || isCreateSessionLoading || isDeletingSession ? (
            <div>
              <CircularProgress />
            </div>
          ) : isError ? (
            <ErrorContainer>Error loading sessions.</ErrorContainer>
          ) : (
            sessions?.map((session, idx) => (
              <li key={idx}>
                <span>
                  <Link to={`session/${session.id}`}> {session.id}</Link>
                </span>
                <span>
                  <Button onClick={() => onSessionDelete(session.id)}>
                    <DeleteIcon />
                  </Button>
                </span>
              </li>
            ))
          )}
        </ul>
        <div
          style={{
            paddingTop: '1rem',
          }}
        >
          <TextField
            variant="standard"
            placeholder="New session"
            value={newSessionId}
            onChange={event => {
              setNewSessionId(event.target.value);
            }}
          />
          <Button variant="contained" onClick={onCreateSession}>
            Create
          </Button>
        </div>
      </div>
    </MenuPage>
  );
};
