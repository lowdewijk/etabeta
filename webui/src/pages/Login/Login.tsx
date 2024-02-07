import React, {useState} from 'react';
import {useNavigate} from 'react-router-dom';
import {Button, TextField} from '@mui/material';

import {useLoggedOutAuth} from '../../auth/AuthProvider';
import {ROUTE_SESSIONS} from '../../routes/Routes';

export const Login = () => {
  const {login} = useLoggedOutAuth();
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  const handleUsernameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setUsername(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login(username);
    navigate(ROUTE_SESSIONS);
  };

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100vh',
      }}
    >
      <div
        style={{
          border: '1px solid black',
          padding: '1rem',
        }}
      >
        <h1>Login</h1>
        <div
          style={{
            paddingTop: '1rem',
          }}
        >
          <form onSubmit={handleSubmit}>
            <label>
              <TextField
                variant="standard"
                placeholder="Username"
                value={username}
                onChange={handleUsernameChange}
              />
            </label>
            <Button type="submit" variant="contained">
              Login
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
