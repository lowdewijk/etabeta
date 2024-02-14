import {FC} from 'react';
import {Route, Routes} from 'react-router-dom';

import {useJoinSession, useLeaveSession} from 'src/api_client/session_queries';
import {useAuth} from 'src/auth/AuthProvider';
import {useRoutePathUpdate} from 'src/generic/useRoutePathUpdate';
import Login from '../pages/Login/Login';
import {SessionsPage} from '../pages/Sessions/SessionsPage';
import {PrivateRoute} from './PrivateRoute';
import {ROUTE_LOGIN, ROUTE_SESSION, ROUTE_SESSIONS} from './Routes';
import {SessionRoute} from './SessionRoute';

const useJoinAndLeaveSessionOnRouteChange = () => {
  const auth = useAuth();
  const {mutate: joinSession} = useJoinSession();
  const {mutate: leaveSession} = useLeaveSession();

  useRoutePathUpdate(
    ROUTE_SESSION,
    ({prevPathMatch, pathMatch}) => {
      if (auth.isLoggedIn) {
        if (prevPathMatch?.params['sessionId'] !== undefined) {
          leaveSession({
            sessionID: prevPathMatch.params['sessionId'],
            username: auth.username,
          });
        }
        if (pathMatch?.params['sessionId'] !== undefined) {
          joinSession({
            sessionID: pathMatch.params['sessionId'],
            username: auth.username,
          });
        }
      }
    },
    [auth, joinSession, leaveSession],
  );
};

export const AppRoutes: FC = () => {
  useJoinAndLeaveSessionOnRouteChange();

  return (
    <Routes>
      <Route path={ROUTE_SESSIONS} element={<PrivateRoute />}>
        <Route path={ROUTE_SESSIONS} element={<SessionsPage />} />
      </Route>
      <Route path={ROUTE_SESSION} element={<PrivateRoute />}>
        <Route path={ROUTE_SESSION} element={<SessionRoute />} />
      </Route>
      <Route path={ROUTE_LOGIN} element={<Login />} />
      <Route path="*" element={<div>404 Not found (react)</div>} />
    </Routes>
  );
};
