import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar.js';
import Header from '../components/Header.js';
import { authorizedAttendanceAPI } from '../Api/Requests';
import { useNavigate, Link } from 'react-router-dom'

function Home() {

	const [courses, setCourses] = useState([]);
	const history = useNavigate()

	function isAuthorized() {
		try {
			if (!localStorage.getItem('token')){
				history('/login')
			}
		} catch (error) {}
	}

	const loadCourses = async () => {
		try {
			const { data } = await authorizedAttendanceAPI.listCourses();
			setCourses(data);
			console.log(data);
		} catch (error) {
			console.log(error);
		}
	};

	function handleEndSession(courseId) {
		try {
			authorizedAttendanceAPI.endSession(courseId);
			window.location.reload();
		} catch (error) {
			console.log(error);
		}
	}

	useEffect(() => {
		isAuthorized();
		loadCourses();
	}, []);

	return (
		<>
			<Navbar />
			<div className="relative md:ml-64 bg-gray-900 p-1">
				<Header />
				<div className="relative bg-gradient-to-r from-gray-800 to-purple-900 md:pt-32 pb-32 pt-12 rounded-2xl">
					<div className="w-full pr-4 mb-16 max-w-full flex-grow flex-auto">
						<span className="flex justify-center uppercase text-white mr-0 whitespace-no-wrap text-3xl font-bold px-0">
							Current Classes
						</span>
						<span className="flex justify-center text-white mr-0 whitespace-no-wrap text-sm pt-2">
							Current courses will be showed here
						</span>
					</div>
					<div className="flex flex-wrap px-2">
						{courses.map((course, index) => (
							<div className="w-full lg:w-6/12 xl:w-6/12 px-4 py-4" id="sampleId">
								<div className="relative flex flex-col min-w-0 break-words bg-white rounded-lg mb-6 xl:mb-0 shadow-lg">
									<div className="flex-auto p-4">
										<div className="flex flex-wrap">
											<div className="relative w-full pr-4 max-w-full flex-grow flex-1">
												<h5 className="text-gray-800 uppercase font-bold text-lg">
													{course.name}
												</h5>
												<span className="mt-4 text-sm text-grey-500">
													{course.students.length} Students
												</span>
												<p className="mt-8">
													<div className="flex">
														<Link to={'/viewsession/' + course.id}>
															<button
																className="bg-purple-800 text-white rounded p-2 font-bold text-base transition duration-300 hover:bg-yellow-500 mr-1"
															>
																View History
															</button>
														</Link>
														{course.status === 2 ? (
															<Link to={'/startsession/' + course.id}>
																<button
																	className="bg-purple-800 text-white rounded p-2 font-bold text-base transition duration-300 hover:bg-yellow-500"
																>
																	Start Session
																</button>
															</Link>
														) : (
															<button
																className="bg-purple-800 text-white rounded p-2 font-bold text-base transition duration-300 hover:bg-yellow-500"
																onClick={() => handleEndSession(course.id)}
															>
																End session
															</button>
														)}
													</div>
												</p>
											</div>

											<div className="relative w-auto pl-4 flex-initial">
												<div className=" p-3 text-center inline-flex items-center justify-center w-16 h-16">
													<svg
														class="w-16 h-16"
														fill="none"
														stroke="currentColor"
														viewBox="0 0 24 24"
														xmlns="http://www.w3.org/2000/svg"
													>
														<path
															stroke-linecap="round"
															stroke-linejoin="round"
															stroke-width="2"
															d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
														></path>
													</svg>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</>
	);
}
export default Home;
