import {useState} from 'react';
import {Link} from 'react-router-dom';
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
      Choose a debate session:
      <ul>
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
                <Link to={`session/${session.id}`}> {session.id}</Link>;
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
    </MenuPage>
  );
};
