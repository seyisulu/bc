import React from 'react';

export const Nav20DataSource = {
  isScrollLink: true,
  wrapper: { className: 'header2 home-page-wrapper jrhtw9ph4a-editor_css' },
  page: { className: 'home-page' },
  logo: {
    className: 'header2-logo',
    children:
      '/logo.svg',
  },
  Menu: {
    className: 'header2-menu',
    children: [
      {
        name: 'Content11_0',
        to: 'Content11_0',
        children: 'Create Account',
        className: 'menu-item',
      },
      {
        name: 'Content12_0',
        to: 'Content12_0',
        children: 'Login',
        className: 'menu-item',
      },
    ],
  },
  mobileMenu: { className: 'header2-mobile-menu' },
  menuLink: { children: [] },
};

export const Banner30DataSource = {
  wrapper: { className: 'banner3' },
  textWrapper: {
    className: 'banner3-text-wrapper',
    children: [
      {
        name: 'nameEn',
        className: 'banner3-name-en',
        children: 'Generic Risk Management Application',
      },
      {
        name: 'slogan',
        className: 'banner3-slogan',
        children: 'Riskify',
        texty: true,
      },
      {
        name: 'name',
        className: 'banner3-name',
        children: 'Create an account to get started!',
      },
      { name: 'button', className: 'banner3-button', children: 'Create Account' },
      {
        name: 'time',
        className: 'banner3-time',
        children: '2018.01.06 / 17:59',
      },
    ],
  },
};

export const Content110DataSource = {
  OverPack: {
    className: 'home-page-wrapper content11-wrapper',
    playScale: 0.3,
  },
  titleWrapper: {
    className: 'title-wrapper',
    children: [
      {
        name: 'image',
        children:
          '/afx.svg',
        className: 'title-image',
      },
      { name: 'title', children: 'Title Image', className: 'title-h1' },
      {
        name: 'content',
        children:
          'Generic Risk Manager',
        className: 'title-content',
      },
      {
        name: 'content2',
        children: 'Riskalatr 1.0',
        className: 'title-content',
      },
    ],
  },
  button: {
    className: '',
    children: { a: { className: 'button', href: '#', children: 'Button #' } },
  },
};

export const Footer20DataSource = {
  wrapper: { className: 'home-page-wrapper footer2-wrapper' },
  OverPack: { className: 'home-page footer2', playScale: 0.05 },
  copyright: {
    className: 'copyright',
    children: [
      {
        name: 'copyright',
        children: 'Emmanuel Olowosulu',
        className: 'copyright-text',
      },
    ],
  },
  links: {
    className: 'links',
    children: [
      {
        name: 'weibo',
        href: 'https://www.github.com/seyisulu/bc',
        className: 'links-weibo',
        children:
          '/github.png',
      },
    ],
  },
};
