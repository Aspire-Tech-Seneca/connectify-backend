import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [reviews, setReviews] = useState([]);
  const [form, setForm] = useState({ name: '', comment: '' });

  const fetchReviews = async () => {
    const res = await axios.get('http://localhost:8000/reviews');
    setReviews(res.data);
  };

  useEffect(() => {
    fetchReviews();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.post('http://localhost:8000/reviews', form);
    setForm({ name: '', comment: '' });
    fetchReviews();
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Submit a Review</h2>
      <form onSubmit={handleSubmit}>
        <input
          placeholder="Your name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        /><br />
        <textarea
          placeholder="Your review"
          value={form.comment}
          onChange={(e) => setForm({ ...form, comment: e.target.value })}
          required
        /><br />
        <button type="submit">Submit</button>
      </form>

      <h3>All Reviews</h3>
      {reviews.map((rev, index) => (
        <div key={index}>
          <strong>{rev.name}</strong>: {rev.comment}
        </div>
      ))}
    </div>
  );
}

export default App;
