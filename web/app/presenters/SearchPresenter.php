<?php

declare(strict_types=1);

namespace App\Presenters;

use App\Model\InvertedModel;
use App\Model\SequentialModel;

use Nette;

final class SearchPresenter extends Nette\Application\UI\Presenter {

    // @var InvertedModel
    private $invertedModel;

    // @var SequentialModel
    private $sequentialModel;

    public function injectDependencies(InvertedModel $invertedModel, SequentialModel $sequentialModel) {
        $this->invertedModel = $invertedModel;
        $this->sequentialModel = $sequentialModel;
    }

    public function renderInverted($id) {
        $docToOpen = $this->invertedModel->getDocument($id);

        $similarDocsObject = $this->invertedModel->getSimilarDocuments($id);

        $this->template->openedDoc = $docToOpen;
        $this->template->openedDocId = $id;
        $this->template->similarDocs = $similarDocsObject[0]['docs'];
        $this->template->timing =$similarDocsObject[1];
    }

    // TODO: Implement missing support in Python
    public function renderSequential($id) {
        $docToOpen = $this->sequentialModel->getDocument($id);

        $similarDocsObject = $this->sequentialModel->getSimilarDocuments($id);

        $this->template->openedDoc = $docToOpen;
        $this->template->openedDocId = $id;
        $this->template->similarDocs = $similarDocsObject[0]['docs'];
        $this->template->timing =$similarDocsObject[1];
    }
}