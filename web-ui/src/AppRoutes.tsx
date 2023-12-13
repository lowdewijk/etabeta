import {FC} from 'react';
import {Route, Routes} from 'react-router-dom';

import {Main} from './pages/Main/Main';
import {Session} from './pages/Session/Session';

export const ROUTE__MAIN = '/main';
export const SESSION_MAIN = '/session/:id';

export const AppRoutes: FC = () => {
  return (
    <Routes>
      <Route path={ROUTE__MAIN} element={<Main />} />
      <Route path={SESSION_MAIN} element={<Session />} />
    </Routes>
  );
};
