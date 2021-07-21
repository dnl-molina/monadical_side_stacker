import { render, screen } from '@testing-library/react';
import App from './App';
import Login from './pages/Login';

test('renders login page', () => {
    const {getByText} =render(<App />)
    const h1=getByText(/play Sid/i)
    expect(h1).toHaveTextContent("play Sid");
});
