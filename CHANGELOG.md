# Changelog
지금까지는...

## Added
- 세포 자동자 기반 게임맵과 동굴 생성.
  - Game map and cave are created with cellular automation method.
- 카메라 구현
  - Camera implemented.
- 간단한 전투와 사망 구현
  - Simple combat and death implemented.
- 간단한 메세지 로그
  - Simple message log

## Changed
- 타일셋 크기 32x32에서 16x16로 변경. 32x32도 남아는 있지만 한동안은 16x16 쓸 예정.
  - Tileset size changed from 32x32 to 16x16.
- 카메라 사용 시 가장자리에서 벽이 '번지는' 것 해결
  - Fixed tile 'smearing' on edge when applying camera.

## Removed
- 분산 다중광원 구현 백지화. 구현 난이도가 너무 높은 데다 광원 여럿이 뭉치면 더 밝아진다는 것 말고는 이점이 없음. 무엇보다도 가장자리에서 오류뜨는거 수정하는 게 지나치게 어려움.
- 입력 함수 최신 메소드로 업데이트 백지화. 수정할 것이 지나치게 많음