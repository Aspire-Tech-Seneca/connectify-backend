-- Insert sample user interests into user_interest table
INSERT INTO users_interest (id, name) VALUES 
(1, 'sports'),
(2, 'music'),
(3, 'tech'),
(4, 'art'),
(5, 'travel');


-- Insert sample users into user_userprofile table
INSERT INTO users_userprofile 
(id, password, last_login, is_superuser, username, first_name, last_name, is_staff, 
 is_active, date_joined, email, fullname, age, bio, location, interest_id)
VALUES 
(101, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'test@example.com', 'Test', 'User', false, 
 true, NOW(), 'test@example.com', 'Test User', 20, 'This is a test user.', 'Toronto', 1),

(102, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'alice@example.com', 'Alice', 'Johnson', false, 
 true, NOW(), 'alice@example.com', 'Alice Johnson', 25, 'Software engineer and tech enthusiast.', 'Waterloo', 2),

(103, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'bob@example.com', 'Bob', 'Smith', false, 
 true, NOW(), 'bob@example.com', 'Bob Smith', 30, 'Loves AI and Machine Learning.', 'Vancouver', 1),

(104, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'charlie@example.com', 'Charlie', 'Brown', false, 
 true, NOW(), 'charlie@example.com', 'Charlie Brown', 28, 'Gamer and aspiring game developer.', 'Toronto', 1),

(105, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'john@example.com', 'John', 'Doe', false, 
 true, NOW(), 'john@example.com', 'John Doe', 35, 'Web developer and open-source contributor.', 'Toronto', 2),

(106, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'sam@example.com', 'Sam', 'Smith', false, 
 true, NOW(), 'sam@example.com', 'Sam Smith', 40, 'Loves AI and Machine Learning.', 'Vancouver', 2),

(107, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'eni@example.com', 'Eni', 'Oken', false, 
 true, NOW(), 'eni@example.com', 'Eni Oken', 25, 'Artist and art teacher.', 'Toronto', 1),

(108, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'jill@example.com', 'Jill', 'Johnson', false, 
 true, NOW(), 'jill@example.com', 'Jill Johnson', 30, 'Software engineer and tech enthusiast.', 'Waterloo', 1),

(109, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'zara@example.com', 'Zara', 'Smith', false, 
 true, NOW(), 'zara@example.com', 'Zara Smith', 28, 'Gamer and aspiring game developer.', 'Toronto', 3),

(110, 'pbkdf2_sha256$870000$fixedsalt123456$1t+Dn4j2afKhIQ5c9gFdnJEsYyZGyB7f3eJI7a7roxY=', NULL, false, 'emma@example.com', 'Emma', 'Brown', false, 
 true, NOW(), 'emma@example.com', 'Emma Brown', 35, 'Web developer and open-source contributor.', 'Vancouver', 4);
