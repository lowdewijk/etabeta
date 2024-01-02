import {FC} from 'react';
import {Route, Routes} from 'react-router-dom';

import Login from 'src/pages/Login/Login';
import {Main} from '../pages/Main/Main';
import {PrivateRoute} from './PrivateRoute';
import {ROUTE_LOGIN, ROUTE_MAIN, ROUTE_SESSION} from './Routes';
import {SessionRoute} from './SessionRoute';

export const AppRoutes: FC = () => {
  return (
    <Routes>
      <Route path={ROUTE_MAIN} element={<PrivateRoute />}>
        <Route path={ROUTE_MAIN} element={<Main />} />
      </Route>
      <Route path={ROUTE_SESSION} element={<PrivateRoute />}>
        <Route path={ROUTE_SESSION} element={<SessionRoute />} />
      </Route>
      <Route path={ROUTE_LOGIN} element={<Login />} />
      <Route path="*" element={<div>404 Not found (react)</div>} />
    </Routes>
  );
};
