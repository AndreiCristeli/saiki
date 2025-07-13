/** 
 * @file frontend/site/script/translate.js
 * 
 * @author AndreiCristeli
 * 
 * @version 0.1
 */

i18next.init({
    lng: 'pt', // Initial language
    debug: true,
  	resources
	}, function(err, t) {
  		updateContent();
	});

function updateContent() {
	document.querySelector('h1').textContent = i18next.t('title');
  	document.querySelector('p').textContent = i18next.t('question');
  	document.querySelector('.Input').placeholder = i18next.t('inputPlaceholder');
  	document.querySelector('.attempts-label').textContent = i18next.t('attempts');

  	const labels = document.querySelectorAll('.label li');
  	const keys = [
    	'categoryInfoTitle',
    	'yearInfoTitle',
    	'timeInfoTitle',
    	'spaceInfoTitle',
    	'structureInfoTitle',
    	'solutionInfoTitle',
    	'generalityInfoTitle'
  	];

  	labels.forEach((el, idx) => {
    	el.textContent = i18next.t(keys[idx]);
  	});

  	document.querySelector('.howToPlayTitle').textContent = i18next.t('howToPlay');
  	document.querySelector('.howToPlayDesc').textContent = i18next.t('description');

  	document.querySelector('.categoryTitle').textContent = i18next.t('categoryInfoTitle');
  	document.querySelector('.categoryText').textContent = i18next.t('categoryInfoText');

  	document.querySelector('.yearTitle').textContent = i18next.t('yearInfoTitle');
  	document.querySelector('.yearText').textContent = i18next.t('yearInfoText');

  	document.querySelector('.timeTitle').textContent = i18next.t('timeInfoTitle');
  	document.querySelector('.timeText').textContent = i18next.t('timeInfoText');

  	document.querySelector('.spaceTitle').textContent = i18next.t('spaceInfoTitle');
  	document.querySelector('.spaceText').textContent = i18next.t('spaceInfoText');

  	document.querySelector('.structureTitle').textContent = i18next.t('structureInfoTitle');
  	document.querySelector('.structureText').textContent = i18next.t('structureInfoText');

  	document.querySelector('.solutionTitle').textContent = i18next.t('solutionInfoTitle');
  	document.querySelector('.solutionText').textContent = i18next.t('solutionInfoText');

  	document.querySelector('.generalityTitle').textContent = i18next.t('generalityInfoTitle');
  	document.querySelector('.generalityText').textContent = i18next.t('generalityInfoText');
}

export function changeLanguage(lang) {
	i18next.changeLanguage(lang, () => {
    	updateContent();
  	});
}