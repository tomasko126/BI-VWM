<?php

declare(strict_types=1);

namespace App\Presenters;

use App\Model\DocumentsModel;
use App\Model\HomepageModel;
use Nette;

final class SearchPresenter extends Nette\Application\UI\Presenter {

    // @var DocumentsModel
    private $documentsModel;

    public function injectDependencies(DocumentsModel $documentsModel) {
        $this->documentsModel = $documentsModel;
    }

    public function renderInverted($id) {
        $docToOpen = $this->documentsModel->getDocument($id);

        $similarDocs = $this->documentsModel->getSimilarDocuments($id)['docs'];

        $this->template->openedDoc = $docToOpen;
        $this->template->similarDocs = $similarDocs;
    }

    // TODO: Implement missing support in Python
    public function actionNaive($id) {

    }
}