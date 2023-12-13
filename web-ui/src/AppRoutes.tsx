import {FC} from 'react';
import {Route, Routes} from 'react-router-dom';

import {Main} from './pages/Main/Main';

export const ROUTE__MAIN = '/main';

export const AppRoutes: FC = () => {
  return (
    <Routes>
      <Route path={ROUTE__MAIN} element={<Main />} />
    </Routes>
  );
};
