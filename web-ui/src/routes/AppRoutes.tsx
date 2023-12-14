import {FC} from 'react';
import {Route, Routes} from 'react-router-dom';

import {Main} from '../pages/Main/Main';
import {SessionRoute} from './SessionRoute';

export const ROUTE__MAIN = '/main';
export const ROUTE__SESSION = '/session/:sessionId';

export const AppRoutes: FC = () => {
  return (
    <Routes>
      <Route path={ROUTE__MAIN} element={<Main />} />
      <Route path={ROUTE__SESSION} element={<SessionRoute />} />
    </Routes>
  );
};
