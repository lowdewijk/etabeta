import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';

import {useAuth} from 'src/auth/AuthProvider';
import {ROUTE_MAIN} from 'src/routes/Routes';

export const Login = () => {
  const {login} = useAuth();
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(username);
    navigate(ROUTE_MAIN);
  };

  return (
    <div>
      <h1>Login</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Username:
          <input type="text" value={username} onChange={handleUsernameChange} />
        </label>
        <br />
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
