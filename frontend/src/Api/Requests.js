import axios from 'axios';
import { apiEndPoint } from '../Config/api.js';

const instance = (token) => {
  return axios.create({
    baseURL: apiEndPoint,
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
};

export const authAPI = {
  createUser(body) {
    return instance()
      .post(`/user/create`, body)
      .then((response) => response);
  },
  createToken(body) {
    return instance()
      .post(`/user/token`, body)
      .then((response) => response);
  },
};

export const authorizedUserAPI = {
	updateUser(body, token) {
		return instance(token)
			.put(`/user/me`, body)
			.then((response) => response);
	},
	retrieveUser(token) {
		return instance(token)
			.get(`/user/me`)
			.then((response) => response)
	}
}

export const authorizedAttendanceAPI = {
	listCourses(token) {
		return instance(token)
			.get(`/attendance/courses/`)
			.then((response) => response);
	},
	createCourse(body, token) {
		return instance(token)
			.post(`/attendance/courses/`, body)
			.then((response) => response);
	},
	updateCourse(body, token) {
		return instance(token)
			.put(`/attendance/courses/`, body)
			.then((response) => response);
	},
	retrieveCourse(courseId, token) {
		return instance(token)
			.get(`/attendance/courses` + courseId)
			.then((response) => response);
	},
	deleteCourse(courseId, token) {
		return instance(token)
			.delete(`/attendance/courses` + courseId)
			.then((response) => response);
	}
}