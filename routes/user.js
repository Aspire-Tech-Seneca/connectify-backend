const express = require('express');
const router = express.Router();
const User = require('../models/User');
const authMiddleware = require('../middleware/auth');

// GET /api/user/profile
router.get('/profile', authMiddleware, async (req, res) => {
  try {
    const user = await User.findById(req.user.userId).select('fullName age bio picture');
    if (!user) return res.status(404).json({ msg: 'User not found' });

    res.status(200).json({
      name: user.fullName,
      age: user.age,
      bio: user.bio,
      picture: user.picture
    });
  } catch (error) {
    console.error(error);
    res.status(500).send('Server error');
  }
});

// PUT /api/user/profile
router.put('/profile', authMiddleware, async (req, res) => {
    const { bio, picture } = req.body;
  
    try {
      // Find user and update bio and picture
      const updatedUser = await User.findByIdAndUpdate(
        req.user.userId,
        { bio, picture },
        { new: true }
      ).select('fullName age bio picture');
  
      if (!updatedUser) return res.status(404).json({ msg: 'User not found' });
  
      res.status(200).json({
        msg: 'Profile updated successfully',
        profile: {
          name: updatedUser.fullName,
          age: updatedUser.age,
          bio: updatedUser.bio,
          picture: updatedUser.picture
        }
      });
    } catch (error) {
      console.error(error);
      res.status(500).send('Server error');
    }
  });  

module.exports = router;
