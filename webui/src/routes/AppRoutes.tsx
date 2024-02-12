import {FC, useEffect, useRef} from 'react';
import {matchPath, Route, Routes, useLocation} from 'react-router-dom';

import {useJoinSession, useLeaveSession} from 'src/api_client/session_queries';
import {useAuth} from 'src/auth/AuthProvider';
import Login from '../pages/Login/Login';
import {SessionsPage} from '../pages/Sessions/SessionsPage';
import {PrivateRoute} from './PrivateRoute';
import {ROUTE_LOGIN, ROUTE_SESSION, ROUTE_SESSIONS} from './Routes';
import {SessionRoute} from './SessionRoute';

const useJoinAndLeaveSessionOnRouteChange = () => {
  const location = useLocation();
  const sessionPath = matchPath(ROUTE_SESSION, location.pathname);
  const {mutate: joinSession} = useJoinSession();
  const {mutate: leaveSession} = useLeaveSession();
  const auth = useAuth();
  const prevSessionId = useRef<string | undefined>();

  useEffect(() => {
    if (!auth.isLoggedIn) return;
    const sessionId = sessionPath?.params.sessionId;
    if (sessionPath && sessionId) {
      if (prevSessionId.current !== sessionId) {
        joinSession({sessionID: sessionId, username: auth.username});
      }
    } else if (prevSessionId.current) {
      leaveSession({sessionID: prevSessionId.current, username: auth.username});
    }
    prevSessionId.current = sessionId;
  }, [sessionPath, prevSessionId, auth, joinSession, leaveSession]);
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
