<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <!-- <a href="https://github.com/UASTARR/STARRGazer">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h3 align="center">STARRGazer</h3>

  <p align="center">
    A ground station system for tracking sounding rockets!
    <br />
    <a href="https://github.com/UASTARR/STARRGazer"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/UASTARR/STARRGazer">View Demo</a>
    &middot;
    <a href="https://github.com/UASTARR/STARRGazer/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/UASTARR/STARRGazer/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <!-- <li><a href="#usage">Usage</a></li> -->
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started. To avoid retyping too much info, do a search and replace with your text editor for the following: `project_description`, `project_license`

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



### Built With

[![Flutter][Flutter.dev]][Flutter-url]  
[![Nginx][Nginx]][Nginx-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

Enviornment
- Ubuntu

You will need git to clone the repo
* git
  ```sh
  sudo apt install git
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/UASTARR/STARRGazer.git
   ```
2. Install the required packages (Needs sudo permission)
   ```sh
   sudo chmod +x ./install.sh
   sudo bash install.sh
   ```

3. Modify nginx config in `/etc/nginx/nginx.conf`
  ```nginx
  rtmp {
        server {
                listen 1935;
                chunk_size 4096;

                application live {
                        live on;
                        record off;
                }
        }
  }

  http {
      ...
      ##
      # RTMP server settings
      ##
      server {
                listen 8080;

                location /hls {
                types {
                        application/vnd.apple.mpegurl m3u8;
                        video/mp2t ts;
                }
                root /var/www/html;
                add_header Cache-Control no-cache;
                }
        }
  }
  ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
<!-- ## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- ROADMAP -->
## Roadmap

- [ ] GPS Display
- [ ] Hardware Control
    - [ ] GPIO Input
- [ ] Live Streaming Server
    - [ ] GPS/Telementry data display
    - [ ] Ground camera dsiplay
    - [ ] Rocket onboard camera display

See the [open issues](https://github.com/UASTARR/STARRGazer/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

### Top contributors:

<a href="https://github.com/UASTARR/STARRGazer/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=UASTARR/STARRGazer" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
<!-- ## License

Distributed under the project_license. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p> -->



<!-- CONTACT -->
## Contact

UASTARR - [website](https://www.uastarr.ca/)

Project Link: [https://github.com/UASTARR/STARRGazer](https://github.com/UASTARR/STARRGazer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

<!-- Accessed 2025-04-25 -->
* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
<!-- https://shields.io/badges/static-badge -->
<!-- https://simpleicons.org/ -->
[contributors-shield]: https://img.shields.io/github/contributors/UASTARR/STARRGazer.svg?style=for-the-badge
[contributors-url]: https://github.com/UASTARR/STARRGazer/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/UASTARR/STARRGazer.svg?style=for-the-badge
[forks-url]: https://github.com/UASTARR/STARRGazer/network/members
[stars-shield]: https://img.shields.io/github/stars/UASTARR/STARRGazer.svg?style=for-the-badge
[stars-url]: https://github.com/UASTARR/STARRGazer/stargazers
[issues-shield]: https://img.shields.io/github/issues/UASTARR/STARRGazer.svg?style=for-the-badge
[issues-url]: https://github.com/UASTARR/STARRGazer/issues
[license-shield]: https://img.shields.io/github/license/UASTARR/STARRGazer.svg?style=for-the-badge
[license-url]: https://github.com/UASTARR/STARRGazer/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://ca.linkedin.com/company/uastarr
[product-screenshot]: images/screenshot.png
[Flutter.dev]: https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white
[Flutter-url]: https://flutter.dev/
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[Nginx]: https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white
[Nginx-url]: https://nginx.org/en/