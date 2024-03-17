import React from 'react';
import { Link } from 'react-router-dom';
import { NavbarDataTeacher } from './NavbarData';

function Navbar() {
	return (
		<>
			<nav className="md:left-0 md:block md:fixed md:top-0 md:bottom-0 md:overflow-y-auto md:flex-row md:flex-no-wrap md:overflow-hidden shadow-xl bg-gray-900 flex flex-wrap items-center justify-between relative md:w-64 z-10 py-4 pr-4">
				<div className="md:flex-col md:items-stretch md:min-h-full md:flex-no-wrap px-0 flex flex-wrap items-center justify-between w-full mx-auto">
					{/* Brand */}
					<Link
						className="md:block text-left md:pb-2 text-white mr-0 inline-block whitespace-no-wrap text-2xl font-bold p-4 mt-4"
						to="/"
					>
						Attendence Portal
					</Link>

					<div
						className={
							'md:flex md:flex-col md:items-stretch md:opacity-100 md:relative md:mt-12 md:shadow-none shadow absolute top-0 left-0 right-0 z-40 overflow-y-auto overflow-x-hidden h-auto items-center flex-1'
						}
					>
						{/* Navigation */}

						<ul className="md:flex-col md:min-w-full flex flex-col list-none">
							{
								NavbarDataTeacher.map((item, index) => (
									<li className="items-center">
										<Link
											className="text-white rounded-r-xl hover:bg-purple-900 text-base py-3 pl-5 mb-6 font-bold block items-center  whitespace-nowrap space-x-3"
											to={item.path}
										>
											<span>{item.icon}</span>
											<span>{item.title}</span>
										</Link>
									</li>
								))
							}
						</ul>
					</div>
				</div>
			</nav>
		</>
	);
}
export default Navbar;
