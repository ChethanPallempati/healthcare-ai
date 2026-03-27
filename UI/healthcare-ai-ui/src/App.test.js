import { render, screen } from '@testing-library/react';
import App from './App';

beforeEach(() => {
  window.localStorage.clear();
});

test('renders login screen', () => {
  render(<App />);
  expect(screen.getByText(/healthcare risk prediction login/i)).toBeInTheDocument();
  expect(screen.getByPlaceholderText(/enter user id/i)).toBeInTheDocument();
});
